def serialize_comment(comment):
    print("commenttttttttttt", comment)
    return {
        'id': str(comment['id']),
        'user': comment['user'],
        'message': str(comment['message'])  # Convert UUID to string
    }