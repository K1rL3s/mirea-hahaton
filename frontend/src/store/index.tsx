import { configureStore } from "@reduxjs/toolkit";

import { advancedSettingsSlice, globalSlice, scanSlice } from "./slices";

export const store = configureStore({
  reducer: {
    globalSlice,
    scanSlice,
    advancedSettingsSlice,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
