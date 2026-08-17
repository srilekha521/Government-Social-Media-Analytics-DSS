from database.database import supabase

response = (
    supabase
    .table("social_media_posts")
    .select("*")
    .limit(5)
    .execute()
)

print("Supabase connection successful!")
print("Data:")
print(response.data)