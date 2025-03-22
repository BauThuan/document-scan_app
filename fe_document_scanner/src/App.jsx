import { useState, useEffect } from 'react'
import { getTest, uploadImage } from './services/services'
import { Upload, Button, message } from "antd";
import { UploadOutlined } from "@ant-design/icons"
import './App.css'

function App() {
  const [message, setMessage] = useState("");

  const fetchApi = async () => {
    try {
      const res = await getTest()
      setMessage(res.message)
    } catch (error) {
      console.log(error)
    }
  }

  const handleUpload = async (info) => {
    try {
      const formData = new FormData();
      formData.append("image_name", info.file);
      const response = await uploadImage(formData)
      message.success(`Upload thành công: ${response.data.image_path}`);
    } catch (error) {
      message.error("Upload thất bại!");
    }
  };

  useEffect(() => {
    fetchApi()
  }, []);

  console.log(message)

  return (
    <>
      <h1>{message}</h1>
      <Upload customRequest={handleUpload} showUploadList={false}>
        <Button icon={<UploadOutlined />}>
          Upload Ảnh
        </Button>
      </Upload>
    </>
  )
}

export default App
