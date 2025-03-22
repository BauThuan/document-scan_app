import React, { useState } from "react";
import { InboxOutlined, UploadOutlined } from "@ant-design/icons";
import { message, Upload, Button } from "antd";
import { uploadImage } from "../services/services";
import { useLoading, useShowUpload } from "../store";

const { Dragger } = Upload;

export const Content = () => {
    const { setLoading } = useLoading()
    const { setIsShow } = useShowUpload()
    const [file, setFile] = useState(null)

    const props = {
        name: "file",
        maxCount: 1,
        action: false,
        accept: "image/jpeg, image/png",
        beforeUpload: (file) => {
            setFile(file);
            return false;
        },
        onRemove: () => {
            setFile(null)
        }
    }

    const handleUpload = async () => {
        try {
            setLoading(true)
            const formData = new FormData();
            formData.append("image_name", file);
            const response = await uploadImage(formData)
            message.success(`Upload thành công: ${response.data.image_path}`)
            setLoading(false)
            setIsShow(true)
        } catch (error) {
            message.error('Upload thất bại!')
            setLoading(false)
            setIsShow(false)
        }
    };

    return (
        <div style={{ width: 400, margin: "0 auto" }}>
            <Dragger {...props}>
                <p className="ant-upload-drag-icon">
                    <InboxOutlined />
                </p>
                <p className="ant-upload-text">Click hoặc kéo file vào đây để chọn</p>
                <p className="ant-upload-hint">Định dạng file JPEG, PNG</p>
            </Dragger>
            <Button
                type="primary"
                // icon={<UploadOutlined />}
                onClick={handleUpload}
                style={{ marginTop: 16, width: "100%" }}
                disabled={!file}
            >
                Upload image
            </Button>
        </div>
    );
};
