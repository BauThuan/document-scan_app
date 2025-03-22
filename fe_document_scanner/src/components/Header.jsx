import { HeaderConatiner } from "../styles"
import { useShowUpload } from "../store"

export const Header = () => {
    const { setIsShow } = useShowUpload()
    return (
        <HeaderConatiner onClick={() => setIsShow(false)}>
            Document Scanner App
        </HeaderConatiner>
    )
}