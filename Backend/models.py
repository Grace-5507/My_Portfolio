from exts import db


class Portfolio(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    Project = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    

    def __repr___(self):
        return f"<Portfolio {self.project} >"


    def save(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self,project,description):
        self.project = project
        self.description = description

        db.session.commit()
