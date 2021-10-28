import setuptools

setuptools.setup(
    name="flight_booking_html_generator",
    version="1.0.0",
    description="HTML boarding card printer for the simple aircraft flight booking system",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={"flight_booking_html_generator": [
        "templates/*.html"
    ]},
    entry_points={
        "flight_booking.card_generator_plugins": [
            "html = flight_booking_html_generator.boarding_card_generator"
        ]
    }
)
