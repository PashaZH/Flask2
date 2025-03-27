from author import Author
from schema import AuthorSchema
import json

json_data = """
{
   "name": "Ivan",
   "email": "ivan@mail.ru"
}
"""

schema = AuthorSchema()
json_data_as_dict = json.loads(json_data)

result = schema.load(json_data_as_dict)
print(result)


json_data_list = """
[
   {
       "id": 1,
       "name": "Alex",
       "email": "alex@mail.ru"
   },
   {
       "id": 2,
       "name": "Ivan",
       "email": "ivan@mail.ru"
   },
   {
       "id": 4,
       "name": "Tom",
       "email": "tom@mail.ru"
   }
]
"""
#json () many=True
# var1 -экземпляр
# var2 - loads

#var1
authors_schema = AuthorSchema(many=True)
result_one = authors_schema.loads(json_data_list)
print(result_one)

#var2
result_two = schema.loads(json_data_list, many=True)
print(result_two)