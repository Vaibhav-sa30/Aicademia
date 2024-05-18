from quart import Quart, render_template
import asyncio

from engineer import eng_papers
from ethicist import eth_papers
from policyMaker import pol_papers

app = Quart(__name__)

@app.route('/')
async def index():
    engineer_paper = await eng_papers()
    ethicist_paper = await eth_papers()
    policyMaker_paper = await pol_papers()
    return await render_template('index.html', engineer_paper=engineer_paper, ethicist_paper=ethicist_paper, policymaker_paper=policyMaker_paper)

if __name__ == "__main__":
    app.run(debug=True)
