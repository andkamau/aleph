from flask import session, Blueprint, redirect, request
from flask_oauthlib.client import OAuthException
from apikit import jsonify
from functools import wraps

from aleph import authz
from aleph.model import Role
from flask.ext.login import login_user
from aleph.core import (db, url_for, oauth_provider,
        system_role, googlelogin)
from aleph.views.cache import enable_cache


blueprint = Blueprint('sessions', __name__)

@blueprint.before_app_request
def load_role():
    request.auth_roles = set([system_role(Role.SYSTEM_GUEST)])
    request.auth_role = None
    request.logged_in = False

    auth_header = request.headers.get('Authorization')

    if session.get('user'):
        request.auth_roles.update(session.get('roles', []))
        request.auth_role = Role.by_id(session.get('user'))
        request.logged_in = True
    elif auth_header is not None:
        if not auth_header.lower().startswith('apikey'):
            return
        api_key = auth_header.split(' ', 1).pop()
        role = Role.by_api_key(api_key)
        if role is None:
            return
        request.auth_role = role
        request.auth_roles.update([system_role(Role.SYSTEM_USER), role.id])
        request.logged_in = True


@blueprint.route('/api/1/sessions')
def status():
    enable_cache(vary_user=True)
    return jsonify({
        'logged_in': authz.logged_in(),
        'api_key': request.auth_role.api_key if authz.logged_in() else None,
        'role': request.auth_role,
        'roles': list(request.auth_roles),
        'permissions': {
            'watchlists': {
                'read': authz.watchlists(authz.READ),
                'write': authz.watchlists(authz.WRITE)
            },
            'sources': {
                'read': authz.sources(authz.READ),
                'write': authz.sources(authz.WRITE)
            }
        },
        'logout': url_for('.logout')
    })


@blueprint.route('/api/1/sessions/login')
def login():
    return oauth_provider.authorize(url_for('sessions.create_or_update_user'))


@blueprint.route('/api/1/sessions/logout')
def logout():
    authz.require(authz.logged_in())
    session.clear()
    return redirect(url_for('ui'))


@blueprint.route('/api/1/sessions/callback')
def callback():
    resp = oauth_provider.authorized_response()
    if resp is None or isinstance(resp, OAuthException):
        # FIXME: notify the user, somehow.
        return redirect(url_for('ui'))

    session['oauth'] = resp
    session['roles'] = [system_role(Role.SYSTEM_USER)]
    if 'googleapis.com' in oauth_provider.base_url:
        me = oauth_provider.get('userinfo')
        user_id = 'google:%s' % me.data.get('id')
        role = Role.load_or_create(user_id, Role.USER, me.data.get('name'),
                                   email=me.data.get('email'))
    elif 'occrp.org' in oauth_provider.base_url or \
            'investigativedashboard.org' in oauth_provider.base_url:
        me = oauth_provider.get('api/2/accounts/profile/')
        user_id = 'idashboard:user:%s' % me.data.get('id')
        role = Role.load_or_create(user_id, Role.USER,
                                   me.data.get('display_name'),
                                   email=me.data.get('email'),
                                   is_admin=me.data.get('is_admin'))
        for group in me.data.get('groups', []):
            group_id = 'idashboard:%s' % group.get('id')
            group_role = Role.load_or_create(group_id, Role.GROUP,
                                             group.get('name'))
            session['roles'].append(group_role.id)
    else:
        raise RuntimeError("Unknown OAuth URL: %r" % oauth_provider.base_url)
    session['roles'].append(role.id)
    session['user'] = role.id
    db.session.commit()
    return redirect(url_for('ui'))


@blueprint.route('/oauth2callback')
@googlelogin.oauth2callback
def create_or_update_user(token, userinfo, **kwargs):
    g_id = userinfo.get('id')
    name = userinfo.get('name')
    email_address = userinfo.get('email')
    user = User.filter_by(google_id=g_id).first()
    if user:
        user.name = username
    else:
        user = User(google_id=g_id,
                    name=username,
                    email=email_address)
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=True)
    return redirect(url_for('ui'))
