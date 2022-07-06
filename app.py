from flask import Flask, jsonify, request
from flask.views import MethodView

from sqlalchemy import Column, Integer, String, DateTime, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


app = Flask('flaskhw')

Base = declarative_base()
engine = create_engine('postgresql://admin:1234@127.0.0.1:5431/flaskhw')
Session = sessionmaker(bind=engine)


class Ads(Base):
    __tablename__ = 'ads'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    description = Column(String, nullable=False)
    date_cr = Column(DateTime, server_default=func.now())
    owner = Column(String, nullable=False)


Base.metadata.create_all(engine)


class AdsView(MethodView):
    def get(self, adv_id: int):
        with Session() as session:
            adv = (session.query(Ads).filter_by(id=adv_id).first())
        return jsonify(
            {
                'id': adv.id,
                'title': adv.title,
                'description': adv.description,
                'date_cr': adv.date_cr,
                'owner': adv.owner
            }
        )

    def post(self):
        adv_new = request.json
        with Session() as session:
            adv = Ads(
                title=adv_new['title'],
                description=adv_new['description'],
                owner=adv_new['owner']
            )
            session.add(adv)
            session.commit()
            return jsonify(
                {
                    'id': adv.id,
                    'title': adv.title,
                    'owner': adv.owner
                }
            )

    def put(self, adv_id: int):
        adv_new = request.json
        with Session() as session:
            session.query(Ads).filter_by(id=adv_id).update(
                {
                    Ads.title: adv_new['title'],
                    Ads.description: adv_new['description']
                }
            )
        return jsonify(
                {
                    'id': adv_id,
                    'title': adv_new['title'],
                    'description': adv_new['description']
                }
            )

    def delete(self, adv_id: int):
        with Session() as session:
            session.query(Ads).filter_by(id=adv_id).delete()
            session.commit()
            return jsonify(
                {
                    'status': f'id {adv_id} - DELETED'
                }
            )


app.add_url_rule('/ads/<int:adv_id>', view_func=AdsView.as_view('show_adv'), methods=['GET'])
app.add_url_rule('/new_adv', view_func=AdsView.as_view('create_adv'), methods=['POST'])
app.add_url_rule('/ads/del/<int:adv_id>', view_func=AdsView.as_view('delete_adv'), methods=['DELETE'])
app.add_url_rule('/ads/edit/<int:adv_id>', view_func=AdsView.as_view('edit_adv'), methods=['PUT'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
