import json
from typing import Optional, Sequence
from langchain.tools.playwright.get_elements import GetElementsTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)


class GetElementsToolUtf8(GetElementsTool):
    def _run(
        self,
        selector: str,
        attributes: Sequence[str] = ["innerText"],
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        results_str = super()._run(selector, attributes, run_manager)
        results = json.loads(results_str)

        return json.dumps(results, ensure_ascii=False)

    async def _arun(
        self,
        selector: str,
        attributes: Sequence[str] = ["innerText"],
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        results_str = await super()._arun(selector, attributes, run_manager)
        results = json.loads(results_str)

        return json.dumps(results, ensure_ascii=False)
