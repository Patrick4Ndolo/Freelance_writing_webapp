from myapp import app
from functools import wraps
from flask import render_template, flash, redirect, url_for, request, abort
from getpass import getpass
from datetime import datetime, timedelta
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, login_required, current_user
import sys
from myapp import db, bcrypt
from myapp.model import User, Writer, Student, Assignment, Post
from flask import current_app
from myapp.forms import LoginForm, ResetPasswordForm, DeleteOrder, UpdateOrder, RegisterForm, ResetPasswordRequestForm, PostAsignmentForm, AssignmentForm, TakeOrder, DeclineOrder
from myapp.email import send_password_reset_email, send_email
from myapp.flask_helper import flash_errors


@app.route('/')
@app.route('/home_page', methods=['GET', 'POST'])
def home_page():
    return render_template('home-page.html')

@app.route('/about', methods=['GET', 'POST'])
def about_page():
    return render_template('about_page.html')

#define a custom decorator to restrict access based on user role

def role_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'admin' in allowed_roles and current_user.role == 'admin':
                return func(*args, **kwargs)
    
            if current_user.is_authenticated and current_user.role in allowed_roles:
                return func(*args, **kwargs)
            else:
                flash(f'Access denied. You dont have permission to access this page', category='danger')
                return redirect(url_for('login_page'))
        return wrapper
    return decorator 

@app.route('/admin', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def admin_page():
    form = AssignmentForm()
    if form.validate_on_submit():
        assignments = Assignment(title=form.title.data, subject=form.subject.data, word_count=form.word_count.data,
                    order_id=form.order_id.data, pages=form.pages.data, description=form.description.data, deadline=form.deadline.data,
                    price=form.price.data, assignment_type=form.assignment_type.data, academic_level=form.academic_level.data)
        db.session.add(assignments)
        db.session.commit()
        flash(f'Your assignment has been posted successfully', category='success')
        return redirect(url_for('new_orders'))
    flash_errors(form)
    
        
    return render_template('admin-page.html', form=form)

# Function to get dashboard counts
def get_dashboard_data():
    assignments_in_progress_count = Assignment.query.filter_by(status='in_progress').count()
    assignments_on_revision_count = Assignment.query.filter_by(status='on_revision').count()
    available_orders_count = Assignment.query.filter_by(status='available').count()
    feedback_count = Assignment.query.filter_by(status='feedback').count()

    return {
        'assignments_in_progress_count': assignments_in_progress_count,
        'assignments_on_revision_count': assignments_on_revision_count,
        'available_orders_count': available_orders_count,
        'feedback_count': feedback_count,
    }

# Function to get available assignments
def get_available_assignments():
    return Assignment.query.filter_by(status='available').all()


@app.route('/writer_dashboard')
def writer_dashboard():
    dashboard_data = get_dashboard_data()
    assignments = get_available_assignments()
    assignments_in_progress_count = Assignment.query.filter_by(status='in_progress').count()
    assignments_on_revision_count = Assignment.query.filter_by(status='on_revision').count()
    available_orders_count = Assignment.query.filter_by(status='available').count()
    return {
        'assignments_in_progress_count': assignments_in_progress_count,
        'assignments_on_revision_count': assignments_on_revision_count,
        'available_orders_count': available_orders_count,
        
    }




    return render_template('writer_dashboard.html', dashboard_data=dashboard_data, assignments=assignments)



@app.route('/writers', methods=['GET', 'POST'])
@login_required
@role_required(['writer', 'admin'])
def writer_page():
    Take_form = TakeOrder()
    Decline_form = DeclineOrder()
    
    if request.method == "POST":
        taken_order = request.form.get('taken_order')
        t_assignment = Assignment.query.filter_by(subject=taken_order).first()
        if t_assignment:
            t_assignment.owner_id = current_user.id
            current_user.budget += t_assignment.price
            db.session.commit()
            flash(f'Success! You have taken assignment of order {t_assignment.order_id} at a cost of {t_assignment.price}')
    if request.method == 'GET':
        available_assignments = Assignment.query.filter_by(status='available').all()
        assignments = Assignment.query.filter_by(owner_id=None)
        
    return render_template('writer-dashboard-page.html', assignments=assignments, Take_form=Take_form, available_assignments=available_assignments, Decline_form=Decline_form)


@app.route('/take_assignment/<int:assignment_id>')
@login_required  # Use Flask-Login to ensure the user is logged in as a writer
def take_assignment(assignment_id):
    assignment = Assignment.query.get(assignment_id)
    if assignment and assignment.status == 'available':
        assignment.status = 'taken'
        assignment.writer_id = current_user.id  # Assign the writer to the assignment
        db.session.commit()
        flash('Assignment taken successfully!', 'success')
    return redirect(url_for('writer'))



@app.route('/student_page', methods=['GET', 'POST'])
@login_required
@role_required(['student', 'admin'])
def student_page():
    form = PostAsignmentForm()
    if form.validate_on_submit():
        posts = Post(title=form.title.data, subject=form.subject.data, word_count=form.word_count.data,
                    description=form.description.data, assignment_type=form.assignment_type.data,
                    academic_level=form.academic_level.data, deadline=form.deadline.data, author=current_user)
        db.session.add(posts)
        db.session.commit()
        flash(f'Your assignment has been posted successfully', category='success')
        return redirect(url_for('assignment_page'))
    flash_errors(form)
    
    

        
    return render_template('student-page.html', title='Student Page', form=form)

@app.route('/assignment', methods=['GET', 'POST'])
@login_required
@role_required(['student', 'admin'])
def assignment_page():
    Update_form = UpdateOrder()
    Delete_form = DeleteOrder()
    posts = Post.query.all()
    if request.method == "POST":
        updated_order = request.form.get('updated_order')
        t_assignment = Post.query.filter_by(subject=updated_order).first()
        t_assignment.owner_id = current_user.id

    elif request.method == "POST":
        deleted_order = request.form.get('deleted_order')
        d_assignment = Post.query.filter_by(subject=deleted_order).first()
        d_assignment.owner_id = current_user.id
    
    return render_template('assignment-page.html', Update_form=Update_form, Delete_form=Delete_form, posts=posts)


@app.route('/editor_page', methods=['GET', 'POST'])
@login_required
def editor_page():
    items = [{
        'id': 1, 'subject': 'Nursing', 'Barcode': '8766773', 'Pages': 9, 
        'Word_count': 3000, 'Price': 786, 'Deadline': '5-10-2023'
    }]
    return render_template('editor-page.html', items=items)

@app.route('/services', methods=['GET', 'POST'])
def services_page():
    items = [{
        'id': 1, 'subject': 'Nursing', 'Barcode': '8766773', 'Pages': 9, 
        'Word_count': 3000, 'Price': 786, 'Deadline': '5-10-2023'
    }]
    return render_template('services-page.html', items=items)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user_to_create = User(username=form.username.data, email_address=form.email_address.data, user_count=form.user_count.data, role=form.role.data, password=hashed_password) 
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)

        if User.role == 'admin':
            #check if the number of admins exceeds limit.
            if User.query.filter_by(role='admin').count() >= 1:
                flash("Sorry, the maximum number of admins has been reached. Please choose another role", category='danger')
        # Increment the admin_count
        admin_users = User.query.filter_by(role='admin').all()
        for admin_user in admin_users:
            admin_user.user_count += 1

        db.session.commit()
        flash(f'You are registered as {user_to_create.username}', category="success")

        return redirect(url_for('login_page'))

    flash_errors(form)


    return render_template('registration-page.html', title='Registration Page', form=form)

    

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    """condition to check if user has entered the correct login details"""
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email_address=form.email_address.data).first()
        """this condition checks the user input against the details stored in the database. 
        If the details match, the user will be rediredted to the market page. 
        The validation will be okayed by a flash message indicating that the login was successful"""
        if attempted_user and bcrypt.check_password_hash(attempted_user.password, form.password.data):
            login_user(attempted_user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Success! You are logged in sucessfully as: {attempted_user.username}', category='success')
            if attempted_user and attempted_user.role == 'admin':
                return redirect(url_for('admin_page'))
            if attempted_user and attempted_user.role == 'writer':
                return redirect(url_for('writer_page'))
            elif attempted_user and attempted_user.role == 'student':
                return redirect(url_for('student_page'))
            elif attempted_user and attempted_user.role == 'editor':
                return redirect(url_for('editor_page'))
            

        else:
            flash('Username and password are not matched! Please try again.', category='danger')



    return render_template('login-page.html', form=form)
        
        


@app.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for('home_page'))


@app.route('/update/<int:assignment_id>', methods=['GET', 'POST'])
@login_required
def update(assignment_id):
        post = Post.query.get_or_404(assignment_id)
        if post.author != current_user:
            abort(403)
        form = PostAsignmentForm()
        if form.validate_on_submit():
            # Update the assignment with the new data
            post.title = request.form['title']
            post.subject = request.form['subject']
            post.word_count = request.form['word_count']
            post.description = request.form['description']
            post.assignment_type = request.form['assignment_type']
            post.academic_level = request.form['academic_level']
            
            new_deadline = request.form.get('deadline')
            if new_deadline:
            # Parse the new deadline value from the form
                post.deadline = datetime.strptime(new_deadline, '%Y-%m-%dT%H:%M')

            # Update other assignment attributes in a similar manner

            db.session.commit()
            flash(f'Assignment updated successfully', category='success')
            return redirect(url_for('assignment_page'))

        return render_template('post_assignment_modal.html', form=form, post=post)


@app.route('/delete/<int:assignment_id>', methods=['POST'])
@login_required
def delete(assignment_id):
        post = Post.query.get_or_404(assignment_id)
        if post.author != current_user:
            abort(403)
        db.session.delete(post)
        db.session.commit()
        flash(f'Your post has been deleted successfully', category='success')
        return redirect(url_for('assignment_page'))
    

@app.route('/order_detail/<int:assignment_id>', methods=['GET'])
def order_detail(assignment_id):
    # Logic to fetch assignment details by assignment_id from the database
    
    assignment = Assignment.query.get(assignment_id)
    post = Assignment.query.all()

    # Check if the assignment exists
    if not assignment:
        # Return a 404 Not Found error if the assignment is not found
        abort(404)  
    db.session.commit()

    # Render the assignment detail template with the fetched details
    return render_template('order_detail.html', assignment=assignment, post=post)


@app.route('/new_orders', methods=['GET'])
def new_orders():
    Take_form = TakeOrder()
    Decline_form = DeclineOrder()

    # Logic to fetch assignment details by assignment_id from the database
    new_order_list = Assignment.query.filter_by(status='new').all
    if request.method == "POST":
        taken_order = request.form.get('taken_order')
        t_assignment = Assignment.query.filter_by(subject=taken_order).first()
        if t_assignment:
            t_assignment.owner_id = current_user.id
            current_user.budget += t_assignment.price
            db.session.commit()
            flash(f'Success! You have taken assignment of order {t_assignment.order_id} at a cost of {t_assignment.price}')
    if request.method == 'GET':
        available_assignments = Assignment.query.filter_by(status='available').all()
        assignments = Assignment.query.filter_by(owner_id=None)
    

    # Check if the assignment exists
    if not new_order_list:
        abort(404)  # Return a 404 Not Found error if the assignment is not found
        
    db.session.commit()

    # Render the assignment detail template with the fetched details
    return render_template('new-orders.html', new_orders=new_order_list, assignments=assignments, Take_form=Take_form, available_assignments=available_assignments, Decline_form=Decline_form)


@app.route('/orders_on_revision', methods=['GET'])
def orders_on_revision():
    # Logic to fetch assignment details by assignment_id from the database
    revision_list = Assignment.query.filter_by(status='revision').all
    
    

    # Check if the assignment exists
    if not revision_list:
        abort(404)  # Return a 404 Not Found error if the assignment is not found
        
    db.session.commit()

    # Render the assignment detail template with the fetched details
    return render_template('order-on-revision.html', on_revision=revision_list)


@app.route('/available_orders', methods=['GET'])
def available_orders():
    # Logic to fetch assignment details by assignment_id from the database
    available_list = Assignment.query.filter_by(status='available').all
    
    

    # Check if the assignment exists
    if not available_list:
        abort(404)  # Return a 404 Not Found error if the assignment is not found
        
    db.session.commit()

    # Render the assignment detail template with the fetched details
    return render_template('available-orders.html', available=available_list)

@app.route('/completed_orders', methods=['GET'])
def completed_orders():
    # Logic to fetch assignment details by assignment_id from the database
    completed_list = Assignment.query.filter_by(status='completed').all
    
    

    # Check if the assignment exists
    if not completed_list:
        abort(404)  # Return a 404 Not Found error if the assignment is not found
        
    db.session.commit()

    # Render the assignment detail template with the fetched details
    return render_template('completed-orders.html', completed=completed_list)


@app.route('/orders_in_progress', methods=['GET'])
def orders_in_progress():
    # Logic to fetch assignment details by assignment_id from the database
    progress_list = Assignment.query.filter_by(status='In_progress').all
    
    

    # Check if the assignment exists
    if not progress_list:
        abort(404)  # Return a 404 Not Found error if the assignment is not found
        
    db.session.commit()

    # Render the assignment detail template with the fetched details
    return render_template('orders-in-progress.html', in_progress=progress_list)

@app.route('/disputed_orders', methods=['GET'])
def disputed_orders():
    # Logic to fetch assignment details by assignment_id from the database
    disputed_list = Assignment.query.filter_by(status='disputed').all
    
    

    # Check if the assignment exists
    if not disputed_list:
        abort(404)  # Return a 404 Not Found error if the assignment is not found
        
    db.session.commit()

    # Render the assignment detail template with the fetched details
    return render_template('disputed-orders.html', disputed=disputed_list)


@app.route('/my_bids', methods=['GET'])
def my_bids():
    # Logic to fetch assignment details by assignment_id from the database
    my_bid_list = Assignment.query.filter_by(status='invites').all
    
    

    # Check if the assignment exists
    if not my_bid_list:
        abort(404)  # Return a 404 Not Found error if the assignment is not found
        
    db.session.commit()

    # Render the assignment detail template with the fetched details
    return render_template('my-bids.html', my_bid=my_bid_list)


@app.route('/invites', methods=['GET'])
def invites():
    # Logic to fetch assignment details by assignment_id from the database
    invites_list = Assignment.query.filter_by(status='invite').all
    
    

    # Check if the assignment exists
    if not invites_list:
        abort(404)  # Return a 404 Not Found error if the assignment is not found
        
    db.session.commit()

    # Render the assignment detail template with the fetched details
    return render_template('invites.html', invites=invites_list)


@app.route('/orders_in_review', methods=['GET'])
def orders_in_review():
    # Logic to fetch assignment details by assignment_id from the database
    review_list = Assignment.query.filter_by(status='invite').all
    
    

    # Check if the assignment exists
    if not review_list:
        abort(404)  # Return a 404 Not Found error if the assignment is not found
        
    db.session.commit()

    # Render the assignment detail template with the fetched details
    return render_template('orders-in-review.html', review=review_list)


@app.route('/discarded_orders', methods=['GET'])
def discarded_orders():
    # Logic to fetch assignment details by assignment_id from the database
    discarded_list = Assignment.query.filter_by(status='discarded').all
    
    

    # Check if the assignment exists
    if not discarded_list:
        abort(404)  # Return a 404 Not Found error if the assignment is not found
        
    db.session.commit()

    # Render the assignment detail template with the fetched details
    return render_template('discarded-orders.html', discarded=discarded_list)



# Redirecting to the 'new_orders' endpoint with the assignment_id parameter
@app.route('/redirect_to_new_orders/<int:assignment_id>', methods=['GET'])
def redirect_to_new_orders(assignment_id):
    # Logic to fetch assignment details by assignment_id from the database
    assignment = Assignment.query.get(assignment_id)

    # Check if the assignment exists
    if not assignment:
        abort(404)  # Return a 404 Not Found error if the assignment is not found

    # Redirect to the 'new_orders' endpoint with the assignment_id parameter
    return redirect(url_for('new_orders', assignment_id=assignment_id))




@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    return redirect(url_for('assignment_page'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit:
        writer = Writer.query.filter_by(email=form.email.data()).first()
        student = Student.query.filter_by(email=form.email.data()).first()
        if writer or student:
            send_email(writer, student)
        flash("Check your email for the instructions to reset your password")
        return redirect(url_for('login_page'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)



@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    user = Writer.verify_reset_password_token(token) or Student.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('home_page'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data())
        db.session.commit()
        flash('Your Password has been reset')
        return redirect(url_for('login_page'))
    return render_template('reset_password.html', form=form)

"""Create a new admin user able to view the /reports endpoint."""

