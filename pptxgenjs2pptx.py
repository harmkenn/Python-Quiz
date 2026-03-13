import streamlit as st
import asyncio
import base64
import os
import tempfile
from pyppeteer import launch

# ─────────────────────────────────────────────
# Helper: run PptxGenJS code in headless Chrome v1.1
# ─────────────────────────────────────────────
async def run_pptxgenjs(js_code: str, output_path: str) -> dict:
    """
    Launches a headless Chromium browser, injects PptxGenJS via CDN,
    executes the user's generatePptx() function, and saves the PPTX
    as a base64 string which is then written to output_path.
    """
    browser = await launch(
        headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox"]
    )
    page = await browser.newPage()

    # Collect console messages for debugging
    console_messages = []
    page.on("console", lambda msg: console_messages.append(msg.text))

    # Build a self-contained HTML page that:
    #  1. Loads PptxGenJS from CDN
    #  2. Runs the user code
    #  3. Calls generatePptx() and exports to base64
    html = """
    <!DOCTYPE html>
    <html>
    <head>
      <script src="https://cdn.jsdelivr.net/npm/pptxgenjs@3.12.0/dist/pptxgen.bundle.js"></script>
    </head>
    <body>
      <div id="status">loading</div>
      <script>
        async function main() {
          try {
            // ── User code injected here ──
            USER_CODE_PLACEHOLDER

            // Call the user's generatePptx function
            const pptx = generatePptx();

            // Export as base64 string
            const base64 = await pptx.write({ outputType: 'base64' });
            document.getElementById('status').innerText = 'done';
            window._pptxBase64 = base64;
          } catch(e) {
            document.getElementById('status').innerText = 'error: ' + e.message;
            window._pptxBase64 = null;
          }
        }
        main();
      </script>
    </body>
    </html>
    """.replace("USER_CODE_PLACEHOLDER", js_code)

    # Load the HTML as a data URI
    encoded_html = base64.b64encode(html.encode("utf-8")).decode("utf-8")
    await page.goto(f"data:text/html;base64,{encoded_html}")

    # Wait for the status element to change from 'loading'
    await page.waitForFunction(
        "document.getElementById('status').innerText !== 'loading'",
        timeout=30000
    )

    # Read the status and base64 result
    status = await page.evaluate("document.getElementById('status').innerText")
    pptx_base64 = await page.evaluate("window._pptxBase64")

    await browser.close()

    if pptx_base64 and status == "done":
        # Decode base64 and write to file
        pptx_bytes = base64.b64decode(pptx_base64)
        with open(output_path, "wb") as f:
            f.write(pptx_bytes)
        return {"success": True, "console": console_messages}
    else:
        return {"success": False, "error": status, "console": console_messages}


# ─────────────────────────────────────────────
# Streamlit UI
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PptxGenJS → PPTX Converter",
    page_icon="📊",
    layout="wide"
)

st.title("📊 PptxGenJS → PPTX Converter")
st.markdown(
    "Paste your **PptxGenJS** JavaScript code below. "
    "Make sure your code is wrapped in a function called `generatePptx()` "
    "that returns the `pptx` object."
)

# ── Example code snippet shown by default ──
default_code = """\
function generatePptx() {
  let pptx = new PptxGenJS();

  pptx.defineSlideMaster({
    title: "MASTER_SLIDE",
    background: { color: "FFFFFF" },
    objects: [
      { rect: { x: 0, y: 0, w: "100%", h: 0.75, fill: { color: "003366" } } },
      { text: {
          text: "My Presentation",
          options: { x: 0.5, y: 0.1, w: 9, h: 0.5, color: "FFFFFF",
                     fontSize: 20, bold: true }
        }
      }
    ]
  });

  let slide = pptx.addSlide({ masterName: "MASTER_SLIDE" });

  slide.addText("Hello from PptxGenJS!", {
    x: 1, y: 1.5, w: 8, h: 1,
    fontSize: 36, bold: true, color: "003366", align: "center"
  });

  slide.addText("Generated via Streamlit", {
    x: 1, y: 3, w: 8, h: 0.5,
    fontSize: 18, color: "555555", align: "center"
  });

  return pptx;
}
"""

# ── Code input area ──
js_code = st.text_area(
    "📝 Paste your PptxGenJS code here:",
    value=default_code,
    height=400,
    help="Your code MUST contain a function named generatePptx() that returns the pptx object."
)

# ── Filename input ──
filename = st.text_input(
    "📁 Output filename:",
    value="presentation.pptx",
    help="Name of the downloaded PPTX file."
)
if not filename.endswith(".pptx"):
    filename += ".pptx"

# ── Convert button ──
if st.button("🚀 Convert to PPTX", type="primary"):
    if not js_code.strip():
        st.error("Please paste some PptxGenJS code first.")
    elif "generatePptx" not in js_code:
        st.error("Your code must contain a function named `generatePptx()`.")
    else:
        with st.spinner("⏳ Running PptxGenJS in headless browser..."):
            # Create a temp file for the output
            with tempfile.NamedTemporaryFile(suffix=".pptx", delete=False) as tmp:
                tmp_path = tmp.name

            try:
                # Run the async function using asyncio.create_task()
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(run_pptxgenjs(js_code, tmp_path))

                if result["success"]:
                    # Read the generated PPTX
                    with open(tmp_path, "rb") as f:
                        pptx_bytes = f.read()

                    st.success("✅ PPTX generated successfully!")

                    # Download button
                    st.download_button(
                        label="⬇️ Download PPTX",
                        data=pptx_bytes,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                    )

                    # Show console output if any
                    if result["console"]:
                        with st.expander("🖥️ Console Output"):
                            for msg in result["console"]:
                                st.code(msg)
                else:
                    st.error(f"❌ Conversion failed: {result.get('error', 'Unknown error')}")
                    if result.get("console"):
                        with st.expander("🖥️ Console Output (Debug)"):
                            for msg in result["console"]:
                                st.code(msg)

            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {str(e)}")
            finally:
                # Clean up temp file
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

# ── Instructions ──
with st.expander("ℹ️ How to use this app"):
    st.markdown("""
    1. **Paste** your PptxGenJS JavaScript code into the text area above.
    2. Make sure your code is wrapped in a function called `generatePptx()` that **returns** the `pptx` object.
    3. Enter a **filename** for your download.
    4. Click **Convert to PPTX**.
    5. Click **Download PPTX** to save the file.

    **Example structure:**
    ```javascript
    function generatePptx() {
      let pptx = new PptxGenJS();
      // ... add slides, content, etc.
      return pptx;  // <-- must return pptx!
    }
    ```

    **Requirements:**
    - Your function must be named exactly `generatePptx`
    - It must return the `pptx` object
    - Do NOT call `pptx.writeFile()` — the app handles the export
    """)
