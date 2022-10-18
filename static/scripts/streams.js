const APP_ID = '70e9fcad9c3243cd9e36b60b955e4195'

const CHANNEL = "main"

const TOKEN = "70e9fcad9c3243cd9e36b60b955e4195"

let UID;

const client = AgoraRTC.createClient({mode: 'rtc', codec: 'vp8'})



let localTracks = []
let remoteUsers = {}


let joinAndDisplayLocalStream = async () => {
            UID = await client.join(APP_ID, CHANNEL, TOKEN, null)

            localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()

            let player = `<div class="video_call" id="user-${UID}" ></div>`

            document.getElementByID("video_call_container").insertAdjacentHTML('beforeend', player)

            localTracks[1].play(`user-${UID}`)

            await client.publish([localTracks[0], localTracks[1]])
}

joinAndDisplayLocalStream()


console.log("streams connected")