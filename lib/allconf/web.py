"""
Web interface based on flask
"""
from flask import Flask
from flask_wtf import Form
from wtforms import StringField, SubmitField
from flask import render_template

app = Flask(__name__)
app.debug = True


def generate_form():
    # form_name = type(settings).__name__

    global setting_form
    global long_descriptions
    if setting_form is None:
        class dynamic_form(Form):
            pass
        long_descriptions = ['', ]
        for key, item in vars(settings).iteritems():
            print 'key', key

            if item.comment is not None:
                long_descr = '<div>' + item.comment + '</div><br />'
            else:
                long_descr = ''
            long_descriptions.append(long_descr)

            """
            setattr(dynamic_form,
                    'long_decription' + key,
                    TextAreaField('',
                                  'long description', default=item.comment)
                    )
            """
            long_descriptions.append('')
            setattr(dynamic_form,
                    key, StringField(key, default=item.get))

        setattr(dynamic_form,
                'submit', SubmitField('submit_field'))
        setting_form = dynamic_form

    form = setting_form(csrf_enabled=False)
    return form, long_descriptions


@app.route('/send', methods=['POST', ])
def receive_xml():
    global settings
    filled_form = setting_form(csrf_enabled=False)
    message = ''
    for i in filled_form:
        if hasattr(settings, i.name):
            getattr(settings, i.name).set(i.data, convert=True)
        message += i.name + ' - {0}'.format(i.data) + '<br />\n'
    Z = xml_writer(settings)
    Z.write_to_file('saved_from_web.xml')
    form, long_descriptions = generate_form()
    return render_template('main.html', form=form,
                           items=zip(form, long_descriptions),
                           message=message)


@app.route('/')
def main():
    form, long_descriptions = generate_form()
    return render_template('main.html', form=form,
                           items=zip(form, long_descriptions))

if __name__ == '__main__':
    setting_form = None
    long_descriptions = None
    settings = profil1
    app.run()
