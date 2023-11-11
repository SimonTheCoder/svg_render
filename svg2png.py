import asyncio
import os
from pyppeteer import launch

async def render_svg_to_png(svg_path, output_path):
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({'width': 3840, 'height': 2160})  # Set viewport to 4K resolution

    # Load the SVG file
    await page.goto(f'file://{svg_path}')

    # Wait for the SVG to render
    await page.waitForSelector('svg')

    # Get the SVG element's dimensions
    element_dimensions = await page.evaluate('''
        () => {
            const svg = document.querySelector('svg');
            const rect = svg.getBoundingClientRect();
            return {
                width: rect.width,
                height: rect.height
            };
        }
    ''')

    # Set the page dimensions to match the SVG dimensions
    await page.setViewport({
        'width': int(element_dimensions['width']),
        'height': int(element_dimensions['height'])
    })

    # Take a screenshot of the SVG
    await page.screenshot({'path': output_path})

    await browser.close()

# Usage example
import sys
import tkinter as tk
from tkinter import filedialog

def get_paths_from_args():
    if len(sys.argv) >= 3:
        svg_path = sys.argv[1]
        output_path = sys.argv[2]
    else:
        root = tk.Tk()
        root.withdraw()
        svg_path = filedialog.askopenfilename(title="Select SVG file", filetypes=(("SVG files", "*.svg"), ("All files", "*.*")))
        output_path = filedialog.asksaveasfilename(title="Save PNG file", defaultextension=".png", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
    return svg_path, output_path

svg_path, output_path = get_paths_from_args()
loop = asyncio.get_event_loop()
loop.run_until_complete(render_svg_to_png(svg_path, output_path))
