# app.py
from api import API
from middleware import Middleware


app = API()


class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Processing request", req.url)

    def process_response(self, req, resp):
        print("Processing response", req.url)


def exception_handler(request, response, exception_cls):
    response.text = "Something went wrong! Please contact system admin"


@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"


@app.route("/about")
def about(request, response):
    response.text = "Hello from the ABOUT page"


@app.route("/html")
def html(request, response):
    response.text = "<style>body{background-color:lightblue;}</style><h1>HTML</h1>"


@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}"


@app.route("/book")
class BookResourse:
    def get(self, req, resp):
        resp.text = "Books Page"


@app.route("/template")
def template_handler(req, resp):
    resp.text = app.template("index.html", context={"name": "Alien", "title": "Best Framework"})


@app.route("/exc")
def exception_throwing_handler(request, response):
    raise AssertionError("This handler shouldn't be used")

app.add_exception_handler(exception_handler)
app.add_middleware(SimpleCustomMiddleware)
