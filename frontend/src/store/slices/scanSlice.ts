import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export interface Vulnerability {
  title: string | null;
  description: string | null;
  severity: string | null;
}

export interface Port {
  port: number;
  protocol?: string | null;
  service?: string | null;
  version?: string | null;
  vulnerabilities?: Vulnerability[];
}

export interface IpData {
  ip: string;
  ptr: string;
  ports: {
    open: Port[];
    closed: number[];
  };
  end: boolean;
}

export type ScanData = null | {
  task_id: string;
  end: boolean;
  ips: IpData[];
};

export type Status = "idle" | "loading" | "done";

export interface ScanState {
  data: ScanData;
  status: Status;
}

const initialState: ScanState = { data: null, status: "idle" };

export const scanSlice = createSlice({
  name: "scanScice",
  initialState,
  reducers: {
    setScanData: (state: ScanState, action: PayloadAction<ScanData>) => {
      state.data = action.payload;
    },
    setScanStatus: (state: ScanState, action: PayloadAction<Status>) => {
      state.status = action.payload;
    },
  },
});

export const { setScanData, setScanStatus } = scanSlice.actions;

export default scanSlice.reducer;
