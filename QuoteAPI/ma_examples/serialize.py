from author import Author
from schema import AuthorSchema

author = Author(1, "Alex", "alex5@mail.ru")
author_schema = AuthorSchema()
result = author_schema.dump(author)


print(type(result), result)

authors = [
   Author("1", "Alex"),
   Author("1", "Ivan"),
   Author("1", "Tom")
]

# чтобы обрабатывать список нужно указывать параментр many=True либо,
# var1 - при создании экземпляра
# var2 - при вызове метода loads

#var1
authors_schema = AuthorSchema(many=True)
result_one = author_schema.dump(authors)
print(repr(result_one), type(result_one))
#var2
result_two = author_schema.dump(authors, many=True)
print(repr(result_two), type(result_one))