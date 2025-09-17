export async function processVideo(videoUrl: string){
    const response = await fetch("http://localhost:3000/process/", {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json'
        },
        body: JSON.stringify({"video_url":videoUrl})
    });

    if (!response.ok) {
        const errorResponse = await response.json()
        console.log(`Failed to process video`)
        throw new Error(`Process video failed: ${errorResponse}`)
    }

    return response.json()
}

export async function sendMessage