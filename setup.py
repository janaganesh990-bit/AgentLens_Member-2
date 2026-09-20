from setuptools import setup, find_packages

setup(
    name="agentlens",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "pydantic>=2.0.0",
    ],
    python_requires=">=3.8",
)
