import flask
from flask import jsonify, make_response, request

from data import db_session
from data.jobs import Job

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/add_job', methods=['POST'])
def add_job():
    if not request.json:
        return make_response(jsonify({'error': 'empty request'}), 400)
    if not all(key in request.json for key in
               ['id', 'job', 'work_size', 'collaborators', 'team_leader']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()

    try:
        job = Job(**request.json)
    except TypeError as err:
        return make_response(jsonify({'error': str(err)}), 500)

    if db_sess.query(Job).filter(Job.id == job.id).first():
        return make_response(jsonify({'error': 'id already exist'}), 500)

    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:id>')
def get_job(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Job).get(id)
    if job is None:
        return make_response(jsonify({'error': 'job not exist'}), 400)
    print(job)
    return jsonify(
        {
            'job': job.to_dict(only=(
                'id',
                'team_leader',
                'job',
                'work_size',
                'collaborators',
                'start_date',
                'end_date',
                'is_finished'
            ))
        })


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Job).all()
    return jsonify(
        {
            'jobs': [item.to_dict(only=(
                'id',
                'team_leader',
                'job',
                'work_size',
                'collaborators',
                'start_date',
                'end_date',
                'is_finished'
            )) for item in jobs]  # only=('title', 'content', 'user.name')
        }
    )
