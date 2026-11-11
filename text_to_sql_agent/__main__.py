import sys 
from pydantic import ValidationError
from text_to_sql_agent.config import Settings 

def main()->None :
 try: settings=Settings()
 except ValidationError as exc:
    print("Configuration invalide:",file=sys.stderr)
    for err in exc.errors():
       print(f"{err['loc'][0]}:{err['msg']}")
    sys.exit(1)
 print(f"Configuration OK :{settings.model_provider}")
 
if __name__=="__main__":
 main()
