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
        id_ = str(get_id(get_from_file('story.csv')))
        fieldnames = [id_, title, story, criteria, bus_val, estimation, status]
        create_data = create(get_from_file('story.csv'), id_, fieldnames)
        write_to_file('story.csv', create_data)
        return render_template("form.html")


@app.route('/story/<story_id>', methods=['POST', 'GET'])
def update_story(story_id=None):
    if request.method == 'GET':
        id_data = get_from_file('story.csv')
        for line in id_data:
            if line[0] == story_id:
                return render_template("form.html", story_id=story_id, title=line[1], story=line[2], criteria=line[3],
                                       bus_value=line[4], estimation=line[5], status=line[6])

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


@app.route('/list', methods=['GET'])
def get_list():
    if request.method == 'GET':
        list_data = get_from_file('story.csv')
        return render_template("list.html", list_data=list_data)


@app.route('/list', methods=['POST'])
def delete_story():
    id_ = request.form['delete_story']
    delete_data = remove(get_from_file('story.csv'), id_)
    write_to_file('story.csv', delete_data)
    list_data = get_from_file('story.csv')
    return render_template("list.html", list_data=list_data)

# generate id, new id based on the max element in id list, (max element+1)


def get_id(id_data):
    id_ = ['0']
    for data in id_data:
        id_.append(data[0])
    max_id = max(map(int, id_))
    return (int(max_id) + 1)

# open writable csv file


def write_to_file(file_name, data):
    with open(file_name, "w") as file:
        for record in data:
            row = ','.join(record)
            file.write(row + "\n")

# open readable csv file


def get_from_file(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
        data = [element.replace("\n", "").split(",") for element in lines]
    return data

# add new story to the database


def create(file_data, id_, field):
    add_data = [n for n in field]
    file_data.append(add_data)
    return file_data

# update story data in story database based on story_id


def update(file_data, id_, field):
    for index, elements in enumerate(file_data):
        if elements[0] == id_:
            update_data = [n for n in field]
            file_data.pop(index)
            file_data.append(update_data)
    return file_data

# delete/remove story data based on story_id


def remove(file_data, id_):
    for index, elements in enumerate(file_data):
        if elements[0] == id_:
            file_data.pop(index)
            return file_data


if __name__ == '__main__':
    app.run(debug=True)
