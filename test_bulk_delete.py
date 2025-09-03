import os
import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
TOKEN = os.getenv("HABISCAN_TOKEN", "")

def get_headers():
    headers = {"Content-Type": "application/json"}
    if TOKEN:
        headers["Authorization"] = f"Token {TOKEN}"
    return headers

def list_images():
    """List all images for the current user"""
    try:
        response = requests.get(f"{BASE_URL}/api/history/images/", headers=get_headers())
        response.raise_for_status()
        data = response.json()
        print(f"Found {data['count']} images:")
        for img in data['results']:
            print(f"  ID: {img['id']}, File: {img['original_filename']}, Uploaded: {img['uploaded_at']}")
        return data['results']
    except Exception as e:
        print(f"Error listing images: {e}")
        return []

def bulk_delete_images(ids):
    """Delete multiple images by IDs"""
    try:
        payload = {"ids": ids}
        response = requests.delete(
            f"{BASE_URL}/api/history/images/bulk_delete/", 
            headers=get_headers(),
            data=json.dumps(payload)
        )
        response.raise_for_status()
        data = response.json()
        print(f"✅ {data['detail']}")
        print(f"   Deleted IDs: {data['deleted_ids']}")
        return True
    except Exception as e:
        print(f"❌ Error deleting images: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Response: {e.response.text}")
        return False

def select_images_to_delete(images):
    """Interactive selection of images to delete"""
    if not images:
        return []
    
    print("\n📋 Select images to delete:")
    print("   Enter numbers separated by commas (e.g., 1,3,5)")
    print("   Enter 'all' to select all images")
    print("   Enter 'none' or press Enter to cancel")
    print()
    
    for i, img in enumerate(images, 1):
        print(f"   {i}. ID: {img['id']} - {img['original_filename']} ({img['uploaded_at'][:10]})")
    
    while True:
        try:
            choice = input("\nYour selection: ").strip().lower()
            
            if choice in ['', 'none', 'cancel']:
                print("❌ Deletion cancelled.")
                return []
            
            if choice == 'all':
                selected = images
                break
            
            # Parse comma-separated numbers
            indices = [int(x.strip()) - 1 for x in choice.split(',')]
            
            # Validate indices
            if any(i < 0 or i >= len(images) for i in indices):
                print("❌ Invalid selection. Please enter valid numbers.")
                continue
            
            selected = [images[i] for i in indices]
            break
            
        except ValueError:
            print("❌ Invalid input. Please enter numbers separated by commas.")
            continue
    
    return selected

def confirm_deletion(selected_images):
    """Ask for confirmation before deletion"""
    if not selected_images:
        return False
    
    print(f"\n⚠️  You are about to delete {len(selected_images)} image(s):")
    for img in selected_images:
        print(f"   • ID: {img['id']} - {img['original_filename']}")
    
    while True:
        confirm = input("\nAre you sure you want to delete these images? (yes/no): ").strip().lower()
        if confirm in ['yes', 'y']:
            return True
        elif confirm in ['no', 'n']:
            print("❌ Deletion cancelled.")
            return False
        else:
            print("Please enter 'yes' or 'no'.")

def main():
    if not TOKEN:
        print("❌ Please set HABISCAN_TOKEN environment variable")
        print("   Example: $env:HABISCAN_TOKEN = 'your_token_here'")
        return
    
    print("🔍 Listing current images...")
    images = list_images()
    
    if not images:
        print("No images found to delete.")
        return
    
    # Interactive selection
    selected_images = select_images_to_delete(images)
    
    if not selected_images:
        return
    
    # Confirmation
    if not confirm_deletion(selected_images):
        return
    
    # Perform deletion
    ids_to_delete = [img['id'] for img in selected_images]
    print(f"\n🗑️  Deleting images with IDs: {ids_to_delete}")
    
    success = bulk_delete_images(ids_to_delete)
    
    if success:
        print("\n🔍 Listing remaining images...")
        list_images()

if __name__ == "__main__":
    main()
