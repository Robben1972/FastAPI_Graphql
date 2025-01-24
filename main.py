import strawberry
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from strawberry.fastapi import GraphQLRouter
from actions.queries import Query
from actions.mutations import Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def home():
    html_content = """
    <html>
        <head>
            <title>Redirect to GraphQL</title>
        </head>
        <body>
            <h1>Welcome to FastAPI with GraphQL</h1>
            <p>Click the button below to go to the GraphQL playground, because this page only for redirecting</p>
            <form action="/graphql">
                <button type="submit">Go to GraphQL</button>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)