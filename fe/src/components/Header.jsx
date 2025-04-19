import { HeaderConatiner } from "../styles"
import { useShowUpload, useFile } from "../store"

export const Header = () => {
    const { setFile } = useFile()
    const { setIsShow } = useShowUpload()
    return (
        <HeaderConatiner onClick={() => {
            setIsShow(false)
            setFile(null)
        }}>
            Document Scanner App
        </HeaderConatiner>
    )
}