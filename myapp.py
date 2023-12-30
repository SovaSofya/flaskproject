from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import func
from models import User, Answers, db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/user/Desktop/программирование/hse_2/flaskproject/myapp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/questionnaire')
def questionnaire():
    return render_template('questionnaire.html')


@app.route('/process', methods=['get'])
def answer_process():
    # если нет ответов, то отсылаем решать анкету
    if not request.args:
        return redirect(url_for('/questionnaire'))

    # достаем параметры
    gender = request.args.get('gender')
    education = request.args.get('education')
    age = request.args.get('age')

    # создаем профиль пользователя
    user = User(
        age=age,
        gender=gender,
        education=education
    )
    # добавляем в базу
    db.session.add(user)
    # сохраняемся
    db.session.commit()
    # получаем юзера с айди (автоинкремент)
    db.session.refresh(user)

    # получаем два ответа
    upper = request.args.get('upper')
    lower = request.args.get('lower')
    whatisbefore = request.args.get('whatisbefore')
    whatisafter = request.args.get('whatisafter')

    # привязываем к пользователю (см. модели в проекте)
    answer = Answers(id=user.id, upper=upper, lower=lower, whatisbefore=whatisbefore, whatisafter=whatisafter)
    # добавляем ответ в базу
    db.session.add(answer)
    # сохраняемся
    db.session.commit()
    return render_template("ending.html")


@app.route('/statistics')
def statistics():
    # заводим словарь для значений (чтобы не передавать каждое в render_template)
    all_info = {}
    age_stats = db.session.query(
        func.avg(User.age),  # средний возраст AVG(user.age)
        func.min(User.age),  # минимальный возраст MIN(user.age)
        func.max(User.age)  # максимальный возраст MAX(user.age)
    ).one()  # берем один результат (он всего и будет один)
    all_info['age_mean'] = age_stats[0]
    all_info['age_min'] = age_stats[1]
    all_info['age_max'] = age_stats[2]
    # это простой запрос, можно прямо у таблицы спросить
    all_info['total_count'] = User.query.count()  # SELECT COUNT(age) FROM user
    answersprim = Answers.query.all()
    answerabsolute = [0, 0, 0, 0]
    answertime = [0, 0, 0, 0]

    for x in answersprim:
        if x.upper == x.lower:
            if x.upper == 'late':
                answerabsolute[0] += 1  # сколько людей считает, что и верхняя, и нижняя граница -- более позднее время
            else:
                answerabsolute[1] += 1  # сколько людей считает, что и верхняя, и нижняя граница -- более раннее время
        else:
            if x.upper == 'late':
                answerabsolute[2] += 1  # сколько людей считает, что верхняя -- позднее время, нижняя -- раннее
            else:
                answerabsolute[3] += 1  # сколько людей считает, что верхняя -- раннее время, нижняя -- позднее

    for x in answersprim:
        if x.whatisbefore == x.whatisafter:
            if x.whatisbefore == 'low':  # сколько людей считает, что и более раннее, и более позднее время -- нижняя граница
                answertime[0] += 1
            else:
                answertime[1] += 1  # сколько людей считает, что и более раннее, и более позднее время -- верхняя граница
        else:
            if x.whatisbefore == 'low':  # сколько людей считает, что более поздняя граница промежутка -- нижняя граница
                answertime[2] += 1
            else:
                answertime[3] += 1  # сколько людей считает, что более поздняя граница промежутка -- верхняя граница

    all_info['ans12'] = answerabsolute  # записываем в словарь, который передадим в шаблон
    all_info['ans34'] = answertime
    # listforplot = [1, 2, 3, 4]  # честное слово, я могла бы сделать график, но у меня анкета немного
    # plt.bar(listforplot, answerabsolute)  # не подходящая для красивой визуализации :(
    # plt.savefig('plot1.jpg')

    return render_template('statistics.html', all_info=all_info)


if __name__ == '__main__':
    app.run(debug=True)
