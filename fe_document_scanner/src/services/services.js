import { HttpRequest } from "../config/axiosConfig"
import { ApiPath } from "./path"

export const getTest = async () => {
    const res = await HttpRequest.get(ApiPath.GET_TEST)
    return res.data
}

export const uploadImage = async (body) => {
    const res = await HttpRequest.post(ApiPath.UPLOAD_IMAGE, body, {
        headers: { "Content-Type": "multipart/form-data" }
    })
    return res
}