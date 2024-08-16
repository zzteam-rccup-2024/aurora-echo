import axios from 'axios'

export function start_record() {
  return axios({
    url: 'http://localhost:8000/record',
    method: 'POST'
  })
}

export async function get_value(key: string) {
  return (await axios('http://localhost:8000/' + key)).data
}

export function start_llm() {
  return axios('http://localhost:8000/llm', {
    method: 'POST'
  })
}

export async function get_llm(perspective: 'object' | 'subject') {
  return (await axios('http://localhost:8000/llm/' + perspective)).data
}

export async function set_llm(product: string) {
  return axios('http://localhost:8000/llm/product', {
    method: 'POST',
    data: {
      product
    }
  })
}

export async function set_mosaic(mosaic: boolean) {
  return axios('http://localhost:8000/mosaic', {
    method: 'POST',
    data: {
      mosaic
    }
  })
}