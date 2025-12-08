# Event Gallery Slideshow Guide

## Overview

Each event now has a beautiful automatic slideshow that displays:
- The main event image
- Gallery images from previous events (uploaded by admin)
- Placeholder slides if no gallery images exist

## Features

✨ **Auto-advancing** - Slides change every 5 seconds  
✨ **Manual navigation** - Click arrows or dots to navigate  
✨ **Pause on hover** - Slideshow pauses when you hover over it  
✨ **Smooth transitions** - Beautiful fade animations  
✨ **Responsive** - Works perfectly on mobile and desktop  
✨ **Dynamic dots** - Navigation dots adjust to number of images  

## How to Add Gallery Images

### Via Admin Panel

1. **Login to Admin**
   - Go to http://127.0.0.1:8000/admin/
   - Login with your superuser credentials

2. **Navigate to Event Gallery**
   - Click on "Event Gallery Images" in the sidebar
   - Or go directly to: http://127.0.0.1:8000/admin/events/eventgallery/

3. **Add New Gallery Image**
   - Click "Add Event Gallery Image" button
   - Select the event from dropdown
   - Upload an image (JPG, PNG, etc.)
   - Add optional caption (e.g., "Last year's amazing crowd!")
   - Set display order (lower numbers appear first)
   - Click "Save"

4. **Add Multiple Images**
   - Repeat step 3 for each image
   - Recommended: 3-6 images per event for best experience

### Image Recommendations

**Size**: 1920x1080px (16:9 ratio) for best results  
**Format**: JPG or PNG  
**File Size**: Under 2MB for fast loading  
**Content**: 
- Crowd shots from previous events
- Performers/speakers in action
- Venue atmosphere
- Happy attendees
- Event highlights

## Display Order

The slideshow displays images in this order:
1. Main event image (from Event model)
2. Gallery images (ordered by the "order" field, then by ID)
3. Placeholder slides (if no gallery images exist)

### Example Order Setup
- Order 0: Opening ceremony
- Order 1: Main performance
- Order 2: Crowd enjoying
- Order 3: Closing moments

## Customization

### Change Auto-Advance Speed

Edit `templates/events/event_detail.html` and find:
```javascript
slideInterval = setInterval(autoSlide, 5000); // 5000 = 5 seconds
```

Change `5000` to your desired milliseconds:
- 3000 = 3 seconds (faster)
- 7000 = 7 seconds (slower)
- 10000 = 10 seconds (much slower)

### Disable Auto-Advance

Remove or comment out these lines:
```javascript
slideInterval = setInterval(autoSlide, 5000);
```

### Change Slideshow Height

Edit the CSS in `templates/events/event_detail.html`:
```html
<div id="slideshow" class="relative h-96 ...">
```

Change `h-96` to:
- `h-64` = shorter (256px)
- `h-80` = medium (320px)
- `h-96` = current (384px)
- `h-[500px]` = custom height

## Troubleshooting

### Images not showing
- Check that images were uploaded successfully in admin
- Verify MEDIA_URL and MEDIA_ROOT in settings.py
- Ensure media folder has write permissions

### Slideshow not advancing
- Check browser console for JavaScript errors (F12)
- Verify JavaScript is enabled in browser
- Clear browser cache and reload

### Dots not appearing
- Check that slides exist (at least 1)
- Verify JavaScript is running (check console)
- Ensure dots-container element exists

## Example Usage

### For a Music Festival
1. Main event poster/banner
2. Last year's crowd shot
3. Headliner performing
4. Food and drinks area
5. Sunset atmosphere
6. Happy attendees

### For a Tech Conference
1. Conference banner
2. Keynote speaker
3. Networking session
4. Workshop in action
5. Exhibition area
6. Panel discussion

### For a Food Festival
1. Festival banner
2. Food stalls
3. Chef demonstrations
4. Happy diners
5. Signature dishes
6. Evening ambiance

## Benefits

✅ **Builds Trust** - Show real photos from previous events  
✅ **Increases Bookings** - Visual proof of great experiences  
✅ **Reduces Questions** - Attendees see what to expect  
✅ **Professional Look** - Modern, engaging presentation  
✅ **Mobile Friendly** - Works perfectly on all devices  

## Tips for Best Results

1. **Use high-quality images** - Clear, well-lit photos
2. **Show variety** - Different angles and moments
3. **Include people** - Happy faces increase conversions
4. **Add captions** - Brief, exciting descriptions
5. **Update regularly** - Add new photos after each event
6. **Test on mobile** - Ensure images look good on small screens

## Future Enhancements (Optional)

- Video support in slideshow
- Lightbox/fullscreen view
- Social media integration
- User-submitted photos
- Instagram feed integration
- Thumbnail navigation

---

**Need help?** Contact: nalisaimbula282@gmail.com | 0978308101
