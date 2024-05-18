from quart import Quart, render_template
import asyncio
from engineer import fetch_paper

app = Quart(__name__)

@app.route('/')
async def index():
    paper_details = await fetch_paper()
    return await render_template('index.html', paper=paper_details)

if __name__ == "__main__":
    app.run(debug=True)
