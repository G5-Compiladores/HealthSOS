import axios from "axios";
const URL_API = "";

export async function getOneMeme(id) {
    try {
      const response = await axios.get(`${URL_API}/${id}`);
      return response.data;
    } catch (error) {
      console.error('Error in the request:', error);
    }
  };

export async function createMeme(dataMeme) {
try {
    
    const response = await axios.post(URL_API, dataMeme)
    .then((response) =>{
    console.log(response);
    });
    return response;
} catch(e) {console.error("ERROR",e);
}
};

export const updateMeme = async (id, dataMeme) => {
    try {
      const response = await axios.put(`${URL_API}/${id}`, dataMeme);
      return response.data;
    } catch (error) {
      console.error(`Error updating user with id ${id}:`, error);
      throw error;
    }
  };

export async function deleteMeme(id) {
    try {
      const response = await axios.delete(`${URL_API}/${id}`);
      return response.data;
    } catch (error) {
      console.error('Error in the request:', error); 
    }
  };
  