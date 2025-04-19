import { Container } from './styles'
import { Content } from './components/Content'
import { Header } from './components/Header'
import { Spin } from 'antd'
import { useLoading } from './store'

function App() {
  const { loading } = useLoading()

  return (
    <Container>
      <Spin spinning={loading}>
        <Header />
        <Content />
      </Spin>
    </Container>
  )
}

export default App
