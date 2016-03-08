from flask import Blueprint, redirect, render_template, request, url_for, flash
from models import Entry, Tag
from helpers import object_list
from forms import EntryForm
from app import db
from sqlalchemy.exc import IntegrityError, InvalidRequestError

entries = Blueprint('entries', __name__, template_folder='templates')


@entries.route('/')
def index():
	entries = Entry.query.order_by(Entry.created_timestamp.desc()).filter(Entry.status == 0)
	return entry_list('entries/index.html', entries)


@entries.route('/tags/')
def tag_index():
	tags = Tag.query.order_by(Tag.name)
	return entry_list('entries/tag_index.html', tags)


@entries.route('/tags/<slug>/')
def tag_detail(slug):
	tag = Tag.query.filter(Tag.slug == slug).first_or_404()
	entries = tag.entries.order_by(Entry.created_timestamp.desc())
	return entry_list('entries/tag_detail.html', entries, tag=tag)


@entries.route('/<slug>/')
def detail(slug):
	# entry = Entry.query.filter(Entry.slug == slug).first_or_404()
	entry = get_entry_or_404(slug)
	return render_template('entries/detail.html', entry=entry)


@entries.route('/create/', methods=['GET', 'POST'])
def create():
	if request.method == 'POST':
		form = EntryForm(request.form)
		if form.validate():
			entry = form.save_entry(Entry())
			try:
				db.session.add(entry)
				db.session.commit()
			except IntegrityError as err:
				db.session.rollback()
				flash('Entry "%s" did not create successfully.' % entry.title, 'warning')
			else:
				flash('Entry "%s" created successfully.' % entry.title, 'success')
				return redirect(url_for('entries.detail', slug=entry.slug))
	else:
		form = EntryForm()
	return render_template('entries/create.html', form=form)


@entries.route('/<slug>/edit/', methods=['GET', 'POST'])
def edit(slug):
	# entry = Entry.query.filter(Entry.slug == slug).first_or_404()
	entry = get_entry_or_404(slug)
	if request.method == 'POST':
		# When WTForms receives an obj parameter, it will attempt to pre-populate the form  fields with values taken from obj
		form = EntryForm(request.form, obj=entry)
		if form.validate():
			entry = form.save_entry(entry)
			try:
				db.session.add(entry)
				db.session.commit()
			except IntegrityError as err:
				db.session.rollback()
				flash('Entry "%s" did not update successfully.' % entry.title, 'warning')
			else:
				flash('Entry "%s" has been saved.' % entry.title, 'success')
				return redirect(url_for('entries.detail', slug=entry.slug))
	else:
		form = EntryForm(obj=entry)
	return render_template('entries/edit.html', entry=entry, form=form)


@entries.route('/<slug>/delete/', methods=['GET', 'POST'])
def delete(slug):
	# entry = Entry.query.filter(Entry.slug == slug).first_or_404()
	entry = get_entry_or_404(slug)
	if request.method == 'POST':
		entry.status = Entry.STATUS_DELETED
		db.session.add(entry)
		db.session.commit()
		flash('Entry "%s" has been deleted.' % entry.title, 'success')
		return redirect(url_for('entries.index'))
	return render_template('entries/delete.html', entry=entry)


def entry_list(template, query, **context):
	valid_statuses = (Entry.STATUS_PUBLIC, Entry.STATUS_DRAFT)
	query = query.filter(Entry.status.in_(valid_statuses))
	if request.args.get('q'):
		search = request.args['q']
		query = query.filter(
			(Entry.body.contains(search)) |
			(Entry.title.contains(search)))
	return object_list(template, query, **context)


def get_entry_or_404(slug):
	valid_statuses = (Entry.STATUS_PUBLIC, Entry.STATUS_DRAFT)
	entry = Entry.query.filter((Entry.slug == slug) & (Entry.status.in_(valid_statuses))).first_or_404()
	return entry
