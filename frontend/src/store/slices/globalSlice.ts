import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";

export interface LastScan {
  task_id: string;
  ip: string;
  updated_at: string;
}

export interface globalState {
  lastScans: LastScan[];
}

const defaultState: globalState = {
  lastScans: [],
};

const initialState: globalState = { ...defaultState };

export const globalSlice = createSlice({
  name: "globalSlice",
  initialState,
  reducers: {
    setLastScans: (state, action: PayloadAction<LastScan[]>) => {
      state.lastScans = action.payload;
    },
  },
});

export const { setLastScans } = globalSlice.actions;

export default globalSlice.reducer;
