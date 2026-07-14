import cv2

# --- CONFIGURATION ---
video_path = r"/home/rudra/projects/youtube-snap/outputs/videos/langchain-job-drafting-loop-video2.mp4"
start_sec = 10  # Start time in seconds
end_sec = 40  # End time in seconds
interval_sec = 5  # Interval in seconds

# Convert seconds to milliseconds for OpenCV
current_msec = start_sec * 1000
end_msec = end_sec * 1000
interval_msec = interval_sec * 1000

# Open the local video
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open the video file.")
    exit()

# Counter for naming your output files sequentially
photo_count = 1

while current_msec <= end_msec:
    # Jump directly to the millisecond position
    cap.set(cv2.CAP_PROP_POS_MSEC, current_msec)

    # Capture the frame
    success, frame = cap.read()
    if not success:
        print(f"Finished or could not read frame at {current_msec // 1000}s.")
        break

    # Save the photo using sequential numbering
    filename = f"frame{photo_count}.png"
    cv2.imwrite(filename, frame)
    print(f"Saved: {filename} (from timestamp {current_msec // 1000}s)")

    # Increment counters for the next step
    photo_count += 1
    current_msec += interval_msec

# Clean up resources
cap.release()
print("All requested photos have been saved successfully!")
