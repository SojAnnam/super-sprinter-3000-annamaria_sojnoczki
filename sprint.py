from flask import Flask
from flask import request
from flask import render_template
import csv

app = Flask(__name__)


@app.route('/story', methods=['POST', 'GET'])
def add_create():
    if request.method == 'GET':
        return render_template("form.html")

    elif request.method == 'POST':
        title = request.form["title"]
        story = request.form["story"]
        criteria = request.form["criteria"]
        bus_val = request.form["bus_value"]
        estimation = request.form["estimation"]
        status = request.form["status"]
        id_ = str(get_id('story.csv'))
        fieldnames = [id_, title, story, criteria, bus_val, estimation, status]
        create_data = create(get_from_file('story.csv'), id_, fieldnames)
        write_to_file('story.csv', create_data)
        return render_template("form.html")


@app.route('/story/<story_id>', methods=['POST', 'GET'])
def update_story(story_id=None):
    if request.method == 'GET':
        id_data = open_csvfile('story.csv')
        for line in id_data:
            data = list(line.strip().split(','))
            if data[0] == story_id:
                return render_template("form.html", story_id=story_id, title=data[1], story=data[2], criteria=data[3],
                                       bus_value=data[4], estimation=data[5], status=data[6])

    elif request.method == 'POST':
        title = request.form["title"]
        story = request.form["story"]
        criteria = request.form["criteria"]
        bus_val = request.form["bus_value"]
        estimation = request.form["estimation"]
        status = request.form["status"]
        id_ = story_id
        fieldnames = [id_, title, story, criteria, bus_val, estimation, status]
        update_data = update(get_from_file('story.csv'), id_, fieldnames)
        write_to_file('story.csv', update_data)
        return render_template("form.html", story_id=story_id)


@app.route('/list', methods=['GET', 'POST'])
def get_list():
    if request.method == 'GET':
        list_data = get_from_file('story.csv')
        print('1')
        return render_template("list.html", list_data=list_data)
    elif request.method == 'POST':
        if request.form['submit'] == '&#10006;':
            id_ = story_id
            print(id_)
            delete_data = remove(get_from_file('story.csv'), id_)
            write_to_file('story.csv', remove_data)
            list_data = get_from_file('story.csv')
            print('ok')
            return render_template("list.html", list_data=list_data)


def get_id(filename):
    with open(filename, 'r') as data:
        id_data = data.readlines()
        lines = 0
        for line in id_data:
            lines += 1
        return (lines + 1)


def open_csvfile(filename):
    with open(filename, 'r') as data:
        id_data = data.readlines()
        return id_data


def write_to_file(file_name, data):
    with open(file_name, "w") as file:
        for record in data:
            row = ','.join(record)
            file.write(row + "\n")


def get_from_file(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
        data = [element.replace("\n", "").split(",") for element in lines]
    return data


def create(file_data, id_, field):
    add_data = [n for n in field]
    file_data.append(add_data)
    return file_data


def update(file_data, id_, field):
    print('2')
    for index, elements in enumerate(file_data):
        if elements[0] == id_:
            update_data = [n for n in field]
            file_data.pop(index)
            file_data.append(update_data)
    return file_data


def remove(file_data, id_):
    for index, elements in enumerate(file_data):
        if elements[0] == id_:
            file_data.pop(index)
            return file_data


if __name__ == '__main__':
    app.run()
