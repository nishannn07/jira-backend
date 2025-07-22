from models.story import Story
from models.epic import Epic
from models import db

def create_story(data, user_id):
    story = Story(
        title=data.get("title"),
        description=data.get("description"),
        status=data.get("status", "todo"),
        priority=data.get("priority", "medium"),
        story_points=data.get("story_points"),
        epic_id=data.get("epic_id"),
        project_id=data.get("project_id")
    )
    db.session.add(story)
    db.session.commit()
    return story

def get_stories_by_epic(epic_id):
    return Story.query.filter_by(epic_id=epic_id, is_deleted=False).all()

def get_stories_by_project(project_id):
    return Story.query.filter_by(project_id=project_id, is_deleted=False).all()

def get_story_by_id(story_id):
    return Story.query.filter_by(id=story_id, is_deleted=False).first()

def update_story(story_id, data, user_id):
    story = Story.query.get_or_404(story_id)
    
    story.title = data.get("title", story.title)
    story.description = data.get("description", story.description)
    story.status = data.get("status", story.status)
    story.priority = data.get("priority", story.priority)
    story.story_points = data.get("story_points", story.story_points)
    
    db.session.commit()
    return story

def delete_story(story_id):
    story = Story.query.get_or_404(story_id)
    story.is_deleted = True
    db.session.commit()
