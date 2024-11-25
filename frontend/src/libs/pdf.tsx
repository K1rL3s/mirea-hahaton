import jsPDF from "jspdf";

import "jspdf-autotable";

// @ts-expect-error idk
import { saveAs } from "file-saver";
import { IpData, Port, ScanData } from "../store/slices/scanSlice";

export const createPDF = (scanData: ScanData) => {
  const doc = new jsPDF();

  if (scanData && scanData.ips) {
    scanData.ips.forEach((ipData: IpData, index) => {
      let currentY = 0;
      if (index !== 0) {
        doc.addPage("a4", "p");
      } else {
        doc.text(`Scan ID: ${scanData.task_id}`, 40, ++currentY * 10);
      }
      doc.text(`IP: ${ipData.ip}`, 10, ++currentY * 10);
      doc.text(`PTR: ${ipData.ptr || "Unknown"}`, 10, ++currentY * 10);

      const openPorts = ipData.ports.open.map((port: Port) => [
        port.port,
        port.protocol || "N/A",
        port.service || "N/A",
        port.version || "N/A",
        port.vulnerabilities?.map((vul) => vul.title).join(", ") || "None",
      ]);

      if (openPorts.length) {
        // @ts-expect-error idk
        doc.autoTable({
          head: [["Port", "Protocol", "Service", "Version", "Vulnerabilities"]],
          body: openPorts,
          startY: ++currentY * 10,
        });
      } else {
        doc.text("Could not found any open ports", 15, ++currentY * 10);
      }
    });
  } else {
    doc.text("No data", 10, 10);
  }

  return doc;
};

export const downloadPDF = (scanData: ScanData) => {
  const data = createPDF(scanData).output("arraybuffer");
  saveAs(
    new Blob([data], { type: "application/pdf" }),
    `${scanData?.task_id}.pdf`,
  );
};

