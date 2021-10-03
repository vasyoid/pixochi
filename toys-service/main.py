import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp


class Appearance(graphene.ObjectType):
    eyes = graphene.Int(description="how many eyes the toy has")
    heads = graphene.Int(description="how many heads the toy has")
    style = graphene.String(description="symbol to draw the toy", default_value="*")


class ToyType(graphene.Enum):
    ANIMAL = 0
    VEHICLE = 1
    DOLL = 2
    CONSTRUCTOR = 3


class Toy(graphene.ObjectType):
    ttype = ToyType(description="animal, car, doll or constructor")
    price = graphene.Int(description="how much the toy costs")
    happiness = graphene.Int(description="how much happier pixochi becomes with the toy")
    appearance = graphene.Field(Appearance)


class Query(graphene.ObjectType):
    toy_by_params = graphene.Field(Toy, ttype=graphene.Int(required=True),
                                   happiness=graphene.Int(required=True),
                                   heads=graphene.Int(required=True))

    @staticmethod
    def resolve_toy_by_params(self, info, ttype, happiness, heads):
        appearance = Appearance(eyes=heads+1, heads=heads)
        return Toy(ttype=ttype, price=10, happiness=happiness, appearance=appearance)


app = FastAPI(title='toys', description='pixochi toys store', version='0.1')
app.add_route("/get-toy", GraphQLApp(schema=graphene.Schema(query=Query)))


@app.get("/")
async def root():
    return {"hello": "world"}
