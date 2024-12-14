frappe.pages['bakong-qr'].on_page_load = function(wrapper) {
	new DepartmentSaleDashboard(wrapper);
};

let DepartmentSaleDashboard = Class.extend({
    // Initialize the dashboard page
    init: function (wrapper) {
        this.page = frappe.ui.make_app_page({
            parent: wrapper,
            title: __("KHQR-BAKONG"),
            single_column: true,
        });
        this.make();
    },


	make: async function () {
        let rendered_html = frappe.render_template("qr", {});
        $(rendered_html).appendTo(this.page.main);

        this.get_books();
    },

})

document.addEventListener("DOMContentLoaded", () => {
    const KHQR = typeof BakongKHQR !== "undefined" ? BakongKHQR : null;

    if (KHQR) {
        const data = KHQR.khqrData;
        const info = KHQR.IndividualInfo;

        const optionalData = {
            currency: data.currency.usd,
            amount: 100.5,
            mobileNumber: "85512233455",
            storeLabel: "Coffee Shop",
            terminalLabel: "Cashier_1",
            purposeOfTransaction: "oversea",
            languagePreference: "km",
            merchantNameAlternateLanguage: "ចទ ស្ទីន",
            merchantCityAlternateLanguage: "សៀមរាប",
            upiMerchantAccount: "0001034400010344ABCDEFGHJIKLMNO",
        };

        const individualInfo = new info(
            "sokha_tim@aclb",
            "Sokha Tim",
            "PHNOM PENH",
            optionalData
        );


        const khqrInstance = new KHQR.BakongKHQR();
        
        const individual = khqrInstance.generateIndividual(individualInfo);

        // Function to display QR code with an image overlay
        const displayQRCode = () => {
            if (individual && individual.data && individual.data.qr) {
                const img = new Image();
                img.src = 'https://cdn-icons-png.flaticon.com/512/5206/5206272.png'; // Set your image path here
                img.onload = () => {
                    const qrCodeCanvas = document.getElementById("qrCodeCanvas");
                    const ctx = qrCodeCanvas.getContext('2d');

                    // Generate the QR code onto the canvas
                    QRCode.toCanvas(
                        qrCodeCanvas,
                        individual.data.qr,
                        function (error) {
                            if (error) {
                                console.error(error);
                                return;
                            }

                            // Draw the logo image in the center of the QR code
                            const qrWidth = qrCodeCanvas.width;
                            const qrHeight = qrCodeCanvas.height;
                            const logoSize = qrWidth / 5; // Adjust the size of the logo (1/5 of the QR code width)
                            const logoX = (qrWidth - logoSize) / 2;
                            const logoY = (qrHeight - logoSize) / 2;

                            ctx.drawImage(img, logoX, logoY, logoSize, logoSize); // Draw the image
                        }
                    );

                    // Show the modal
                    const qrCodeModal = new bootstrap.Modal(
                        document.getElementById("qrCodeModal")
                    );
                    qrCodeModal.show();
                };
            } else {
                console.error("QR code data is not available.");
            }
        };

        // Attach event listeners for the Checkout button
        const checkoutButton = document.getElementById("checkout");
        if (checkoutButton) {
            checkoutButton.addEventListener("click", displayQRCode);
        } else {
            console.error("Checkout button is not available.");
        }
    }
});