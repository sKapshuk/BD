from app import app
from flask import render_template, request, jsonify, Blueprint,abort
from app.utilities import json_to_dict,json_w
from app.view_handlers import get_ticket_handler
from .alch_class import ticket_add,delete_wagone,add_wagons

API_V1 = '/api/v1'
main_blueprint = Blueprint('main', __name__, url_prefix=API_V1)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ticket')
def ticket():
    train = request.args.get('train')
    carriage = request.args.get('carriage')
    place = request.args.get('place')
    if train and carriage and place:
        ticket = get_ticket_handler(data={'train': train, 'carriage': carriage, 'place': place})
        ticket_add(train,carriage,int(place))
        return render_template('ticket.html', ticket=ticket)
    return render_template('ticket.html')


@app.route('/api/<action>', methods=["GET"])
def api_get(action):
    carriage = json_to_dict("app/data_json/carriage.json")
    train = json_to_dict("app/data_json/train.json")
    if action == "carriage":
        idd = request.args.get('idd')
        trai = request.args.get('trai')
        free_pl = request.args.get('free_pl')
        typ = request.args.get('type')
        if idd and trai and free_pl and typ:
            data={"id": idd, "train": trai, "type": typ, "free_places": free_pl}
            json_w("app/data_json/carriage.json",data)

            carriage = json_to_dict("app/data_json/carriage.json")

            return render_template("carriage.html", carriage=carriage)

        return render_template("carriage.html")

    elif action == "train":
        idd = request.args.get('idd')
        station_dep = request.args.get('station_dep')
        station_arr = request.args.get('station_arr')
        data_dep = request.args.get('data_dep')
        data_arr = request.args.get('data_arr')
        if idd and station_dep and station_arr and data_dep and data_arr:
            data = {"id": idd, "station_arrival": station_dep,"station_departure": station_arr,"data_arrival":  data_dep,"data_departure":  data_arr}
            json_w("app/data_json/train.json",data)

            train = json_to_dict("app/data_json/train.json")
            return render_template("train.html", train=train)

        return render_template("train.html")

    elif action == "all":
        return render_template("all.html", train=train, carriage=carriage)

    else:
        abort(404)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main_blueprint.route('/ticket', methods=['POST'])
def get_ticket():
    train = request.args.get('train')
    carriage = request.args.get('carriage')
    place = request.args.get('place')
    app.logger.info(f'get ticket with data: train:{train}, carriage:{carriage}, place:{place}')
    if train and carriage and place:
        return 'True', 200
    return 'False', 400


@main_blueprint.route('/ticket/return', methods=['POST'])
def return_ticket():
    data = request.get_json()
    if data:
        resp = get_ticket_handler(data)
        return jsonify(resp), 200
    return {'result': False}, 400

