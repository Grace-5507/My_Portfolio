from flask import Flask, request
from flask_restx import Api, Resource, fields #Flask_restx provides a coherent collection of decorators and tools to describe  API and expose its documentation properly (using Swagger).
from config import DevConfig
from models import Portfolio
from exts import db

app=Flask(__name__)
app.config.from_object(DevConfig)
api=Api(app, doc="/docs")

db.init_app(app)#Registers SQLAlchemy to work with curent application



#Serializer that will help to serialize/expose/marshal the model into json format
portfolio_model = api.model(
    'Portfolio',
    {
        'id':fields.Integer(),
        'project':fields.String(),
        'description':fields.String()

    }
)

@api.route("/Hello")
class HelloResource(Resource):
    def get(self):
        return {"message":"Hello world"}

@api.route('/portfolios')
class portfoliosResource(Resource):
    @api.marshal_list_with(portfolio_model)#turns sqlalchemy object into a json object that can be used in the front end.
    def get(self):
        #get all projects
        portfolios = Portfolio.query.all()
        return portfolios

    
    @api.marshal_with(portfolio_model)
    @api.expect(portfolio_model)
    
    def post(self):
        #Create a new project
        data = request.get_json()
        new_portfolio = Portfolio(
            project = data.get('project'),
            description = data.get('description')
        )
        new_portfolio.save()

        return new_portfolio, 201


@app.shell_context_processor  #imports the db object, and making it available to the Python interactive shell via the @app.shell_context_processor decorator.(To expose the models via a terminal shell(serializer) to allow for interaction with API methods.)
def make_shell_context():
    return {"db":db,
            "Portfolio":Portfolio
           
        }
if __name__ == '__main__':
    
    app.run()