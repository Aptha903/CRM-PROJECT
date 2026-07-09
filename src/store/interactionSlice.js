
import { configureStore, createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../services/api';

const initialState = {
  interactions: [],
  currentInteraction: null,
  loading: false,
  error: null,
  chatMessages: [],
  showForm: true,
  showChat: false,
};

export const fetchInteractions = createAsyncThunk('interactions/fetchAll', async () => {
  const response = await api.getInteractions();
  return response.data;
});

export const createInteraction = createAsyncThunk('interactions/create', async (interactionData) => {
  const response = await api.createInteraction(interactionData);
  return response.data;
});

export const updateInteraction = createAsyncThunk('interactions/update', async ({ id, data }) => {
  const response = await api.updateInteraction(id, data);
  return response.data;
});

export const deleteInteraction = createAsyncThunk('interactions/delete', async (id) => {
  await api.deleteInteraction(id);
  return id;
});

export const sendChatMessage = createAsyncThunk('interactions/chat', async (message) => {
  const response = await api.sendChatMessage(message);
  return response.data;
});

const interactionSlice = createSlice({
  name: 'interactions',
  initialState,
  reducers: {
    toggleView: (state) => {
      state.showForm = !state.showForm;
      state.showChat = !state.showChat;
    },
    setCurrentInteraction: (state, action) => {
      state.currentInteraction = action.payload;
    },
    addChatMessage: (state, action) => {
      state.chatMessages.push(action.payload);
    },
    clearChat: (state) => {
      state.chatMessages = [];
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchInteractions.pending, (state) => { state.loading = true; })
      .addCase(fetchInteractions.fulfilled, (state, action) => { state.loading = false; state.interactions = action.payload; })
      .addCase(fetchInteractions.rejected, (state, action) => { state.loading = false; state.error = action.error.message; })
      .addCase(createInteraction.fulfilled, (state, action) => { state.interactions.unshift(action.payload); state.currentInteraction = action.payload; })
      .addCase(updateInteraction.fulfilled, (state, action) => {
        const index = state.interactions.findIndex(i => i.id === action.payload.id);
        if (index !== -1) { state.interactions[index] = action.payload; }
        state.currentInteraction = action.payload;
      })
      .addCase(deleteInteraction.fulfilled, (state, action) => {
        state.interactions = state.interactions.filter(i => i.id !== action.payload);
      });
  },
});

export const { toggleView, setCurrentInteraction, addChatMessage, clearChat } = interactionSlice.actions;

export default configureStore({ reducer: { interactions: interactionSlice.reducer } });