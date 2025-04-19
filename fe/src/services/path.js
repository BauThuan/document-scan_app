
export class ApiPath {
    static VERSION = import.meta.env.VITE_API_VERSION_V1;
    // path api
    static GET_TEST = ApiPath.VERSION + 'public/test';
    static UPLOAD_IMAGE = ApiPath.VERSION + 'public/upload-transform';
}
