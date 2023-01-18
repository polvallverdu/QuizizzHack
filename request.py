from pyodide.http import pyfetch
from typing import Optional, Any

async def request(url: str, method: str = "GET", body: Optional[str] = None,
                  headers: Optional[dict[str, str]] = None, **fetch_kwargs: Any) -> dict:
    """
    Async request function. Pass in Method and make sure to await!
    Parameters:
        url: str = URL to make request to
        method: str = {"GET", "POST", "PUT", "DELETE"} from `JavaScript` global fetch())
        body: str = body as json string. Example, body=json.dumps(my_dict)
        headers: dict[str, str] = header as dict, will be converted to string...
            Example, headers=json.dumps({"Content-Type": "application/json"})
        fetch_kwargs: Any = any other keyword arguments to pass to `pyfetch` (will be passed to `fetch`)
    Return:
        response: pyodide.http.FetchResponse = use with .status or await.json(), etc.
    """
    kwargs = {"method": method, "mode": "cors"}  # CORS: https://en.wikipedia.org/wiki/Cross-origin_resource_sharing
    if body and method not in ["GET", "HEAD"]:
        kwargs["body"] = body
    if headers:
        kwargs["headers"] = headers
    kwargs.update(fetch_kwargs)

    response = await pyfetch(url, **kwargs)
    data = await response.json()
    return data

def format_struc(struc: dict) -> dict:
  return {
        "type": struc["type"],
        "text": struc["text"],
        "media": struc["media"],
        "math": struc["math"] if struc["hasMath"] else None
      }

async def format_responses(quiz_id: str, type: str="quizizz") -> dict|None:
  # Sample quizizz_id: 638f4246036b61001daa66e0
  data = await request(f"http://localhost:8080?id={quiz_id}&type={type}")
  
  if not data["success"]:
    return None

  questions = data["data"]["quiz"]["info"]["questions"]
  final_data = []
  
  for question in questions:
    options_scrap = question["structure"]["options"]
    answer_scrap = question["structure"]["answer"]
    query_scrap = question["structure"]["query"]
    
    has_correct_answer_scrap = question["structure"]["settings"]["hasCorrectAnswer"]
    multiple_choice_scrap = question["structure"]["settings"]["doesOptionHaveMultipleTargets"]
    can_submit_custom_response_scrap = question["structure"]["settings"]["canSubmitCustomResponse"]

    ############################################################
    
    ques = format_struc(query_scrap)
    options = []
    answer = answer_scrap  #TODO: Maybe check math type
    
    for option in options_scrap:
      options.append(format_struc(option))
    
    
    final_data.append({
      "question": ques,
      "options": options,
      "answer": answer,
      "has_correct_answer": has_correct_answer_scrap,
      "multiple_choice": multiple_choice_scrap,
      "can_submit_custom_response": can_submit_custom_response_scrap,
    })
  
  return {
    "title": data["data"]["quiz"]["info"]["name"],
    "image": data["data"]["quiz"]["info"]["image"],
    "creator": data["data"]["quiz"]["createdBy"]["local"]["casedUsername"],
    "length": str(len(final_data)),
    "questions": final_data,
  }