from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, date
import calendar
from models import db, Client, Appointment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agenda.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()


def month_calendar(year, month):
    cal = calendar.Calendar(firstweekday=6)  # Domingo primeiro
    return cal.monthdatescalendar(year, month)


@app.route('/')
def index():
    try:
        year = int(request.args.get('year', date.today().year))
        month = int(request.args.get('month', date.today().month))
    except ValueError:
        year, month = date.today().year, date.today().month

    grid = month_calendar(year, month)

    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1)
    else:
        end = datetime(year, month + 1, 1)

    appts = Appointment.query.filter(
        Appointment.starts_at >= start,
        Appointment.starts_at < end
    ).all()

    appts_by_date = {}
    for a in appts:
        d = a.starts_at.date()
        appts_by_date.setdefault(d, []).append(a)

    month_name = calendar.month_name[month]

    return render_template(
        'index.html',
        grid=grid,
        year=year,
        month=month,
        month_name=month_name,
        appts_by_date=appts_by_date
    )


# Clientes
@app.route('/clients')
def clients():
    all_clients = Client.query.all()
    return render_template('clients.html', clients=all_clients)


@app.route('/clients/new', methods=['GET', 'POST'])
def new_client():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        client = Client(name=name, phone=phone, email=email)
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('clients'))
    return render_template('client_form.html', client=None)


@app.route('/clients/edit/<int:client_id>', methods=['GET', 'POST'])
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)
    if request.method == 'POST':
        client.name = request.form['name']
        client.phone = request.form['phone']
        client.email = request.form['email']
        db.session.commit()
        return redirect(url_for('clients'))
    return render_template('client_form.html', client=client)


@app.route('/clients/delete/<int:client_id>')
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('clients'))


'''@app.route("/appointments/new", methods=["GET", "POST"])
def new_appointment():
    if request.method == "POST":
        client = request.form["client"]
        service = request.form["service"]
        date = request.form["date"]
        time = request.form["time"]

        # Aqui você pode salvar no banco (SQLite, por exemplo)
        print(f"Novo agendamento: {client}, {service}, {date} {time}")

        return redirect(url_for("index"))

    return render_template("appointment_form.html", appointment=None)'''


'''# Agendamentos
@app.route('/appointments/new', methods=['GET', 'POST'])
def new_appointment():
    clients_list = Client.query.all()
    if request.method == 'POST':
        client_name = string(request.form['client_id'])
        starts_at_str = request.form['starts_at']
        starts_at = datetime.fromisoformat(starts_at_str)
        description = request.form['description']
        appt = Appointment(client_id=client_id, starts_at=starts_at, description=description)
        db.session.add(appt)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('appointment_form.html', appointment=None, clients=clients_list)'''


# Agendamentos
@app.route('/appointments/new', methods=['GET', 'POST'])
def new_appointment():
    if request.method == 'POST':
        client_name = request.form['client_name']   # Agora é string
        starts_at_str = request.form['starts_at']
        starts_at = datetime.fromisoformat(starts_at_str)
        description = request.form['description']

        # Cria o agendamento com o nome do cliente (string)
        appt = Appointment(
            client=client_name,
            starts_at=starts_at,
            description=description
        )

        db.session.add(appt)
        db.session.commit()
        return redirect(url_for('index'))

    # GET → mostra o formulário
    return render_template('appointment_form.html', appointment=None)


@app.route('/appointments/edit/<int:appt_id>', methods=['GET', 'POST'])
def edit_appointment(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    clients_list = Client.query.all()
    if request.method == 'POST':
        appt.client_id = int(request.form['client_id'])
        appt.starts_at = datetime.fromisoformat(request.form['starts_at'])
        appt.description = request.form['description']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('appointment_form.html', appointment=appt, clients=clients_list)


@app.route('/appointments/delete/<int:appt_id>')
def delete_appointment(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    db.session.delete(appt)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/appointments/<int:appt_id>')
def view_appointment(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    return render_template('appointment_view.html', appt=appt)


if __name__ == '__main__':
    app.run(debug=True)
