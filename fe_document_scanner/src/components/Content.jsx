import React, { useState } from "react";
import { InboxOutlined } from "@ant-design/icons";
import { message, Upload, Button } from "antd";
import { uploadImage } from "../services/services";
import { useLoading, useShowUpload } from "../store";
import { ImageContainer } from "../styles";
import { translations } from "../constant";

const { Dragger } = Upload;

export const Content = () => {
    const { setLoading } = useLoading()
    const { isShow, setIsShow } = useShowUpload()
    const [data, setData] = useState({})
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
            setData(response.data)
            message.success(`Upload thành công`)
            setLoading(false)
            setIsShow(true)
        } catch (error) {
            message.error('Upload thất bại!')
            setLoading(false)
            setIsShow(false)
        }
    };

    return (

        <>
            {isShow
                ? <div>
                    <div style={{ width: "80%", margin: '0 auto', display: 'flex', alignItems: "center", justifyContent: "space-between" }}>
                        <ImageContainer style={{ backgroundImage: `url("data:image/jpeg;base64,${data?.originalImage}")` }} />
                        <span style={{ fontSize: "24px" }}>➡️</span>
                        <ImageContainer style={{ backgroundImage: `url("data:image/jpeg;base64,${data?.boxedImage}")` }} />
                    </div>
                    <div style={{ display: "flex", gap: "20px", flexWrap: "wrap", alignItems: 'center', justifyContent: "center", marginTop: 20 }}>
                        <table
                            border="1"
                            cellPadding="10"
                            style={{
                                borderCollapse: "collapse",
                                width: "50%",
                                backgroundColor: "#1e1e1e",
                                color: "white",
                                border: "1px solid #444"
                            }}
                        >
                            <tbody>
                                {Object.entries(data?.result || {}).map(([key, value]) => {
                                    if (!key.trim()) return null;
                                    return (
                                        <tr key={key}>
                                            <td style={{ textAlign: "left", fontWeight: "bold", backgroundColor: "#333", padding: "10px" }}>
                                                {translations[key] || key}
                                            </td>
                                            <td style={{ textAlign: "left", padding: "10px" }}>
                                                {Array.isArray(value) && value.length ? value.join(", ") : ""}
                                            </td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                </div>
                : <div style={{ width: 500, margin: "0 auto" }}>
                    <Dragger {...props}>
                        <p className="ant-upload-drag-icon">
                            <InboxOutlined />
                        </p>
                        <p className="ant-upload-text">Click hoặc kéo file vào đây để chọn</p>
                        <p className="ant-upload-hint">Định dạng file JPEG, PNG</p>
                    </Dragger>
                    <Button
                        type="primary"
                        onClick={handleUpload}
                        style={{ marginTop: 16, width: "100%" }}
                        disabled={!file}
                    >
                        Upload image
                    </Button>
                </div>}


        </>
    );
};
