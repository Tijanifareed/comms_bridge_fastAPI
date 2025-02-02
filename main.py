from fastapi import FastAPI, File, UploadFile, HTTPException
from comms_bridge.audio_dectect_service import AudioDectect


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/process/area/audio")
async def process_audio(file: UploadFile = File(...)):
    class_map_file = "yamnet_class_map.csv"

    try:
        # Check if file is provided
        if not file:
            raise HTTPException(status_code=400, detail="No file part in the request")

        audio_dectect = AudioDectect()
        result = audio_dectect.identify_sound(file.file, class_map_file)
        print(result)

        return {"status": "success", "message": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
