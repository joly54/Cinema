import React from 'react'
import {ComponentPreview, Previews} from '@react-buddy/ide-toolbox'
import {PaletteTree} from './palette'
import Profile from "../components/Profile";
import SesInfo from "../components/SesInfo";

const ComponentPreviews = () => {
    return (
        <Previews palette={<PaletteTree/>}>
            <ComponentPreview path="/Profile">
                <Profile/>
            </ComponentPreview>
            <ComponentPreview path="/SesInfo">
                <SesInfo/>
            </ComponentPreview>
        </Previews>
    )
}

export default ComponentPreviews