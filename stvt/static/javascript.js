 <html>
    <head></head>
    <body>
      <button id="downloadBtn" onclick="downloadPDF()">Download Certificate</button>    
       <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
 <script>
    async function downloadPDF() {
  const { jsPDF } = window.jspdf;
  const element = document.getElementById("certificate");

  await html2canvas(element, {
    scale: 2,
    useCORS: true
  }).then(canvas => {
    const imgData = canvas.toDataURL("image/png", 1.0);
    const pdf = new jsPDF("landscape", "pt", "a4");

    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();

    // Padding (in pt)
    const padding = 30;

    const imgWidth = pageWidth - 2 * padding;
    const imgHeight = (canvas.height * imgWidth) / canvas.width;

    const x = padding;
    const y = (pageHeight - imgHeight) / 2;  // Center vertically

    pdf.addImage(imgData, "PNG", x, y, imgWidth, imgHeight);
    pdf.save("Certificate.pdf");
  });
}

  </script>
  </body>

</html>
